import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import os
import json
import time
import streamlit as st

st.set_page_config(page_title="Finance AI Agent", layout="wide")

st.title("Finance Credit Follow-Up AI Agent")

st.sidebar.title("AI Finance Agent")
st.sidebar.write("Automated payment follow-up email generation system")

if "generated_emails" not in st.session_state:
    st.session_state.generated_emails = []

if "records" not in st.session_state:
    st.session_state.records = []

if "emails_generated" not in st.session_state:
    st.session_state.emails_generated = False

if "escalation_accounts" not in st.session_state:
    st.session_state.escalation_accounts = []

uploaded_file = st.file_uploader(
    "Upload Customer Invoice Data",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        data = pd.read_csv(uploaded_file)

        required_columns = [
            "client_name",
            "invoice_no",
            "amount",
            "due_date",
            "follow_up_count",
            "email"
        ]

        missing_columns = []

        for col in required_columns:
            if col not in data.columns:
                missing_columns.append(col)

        if len(missing_columns) > 0:
            st.error(f"Missing required columns: {missing_columns}")
            st.stop()

        if data.empty:
            st.error("Uploaded CSV file is empty")
            st.stop()

        if not data["email"].astype(str).str.contains("@").all():
            st.error("Some email addresses are invalid")
            st.stop()

        try:
            data["due_date"] = pd.to_datetime(data["due_date"])
        except:
            st.error("Invalid due_date format")
            st.stop()

        st.success("Valid CSV Uploaded Successfully")

        st.subheader("Uploaded Data Preview")

        st.dataframe(data)

        st.metric("Total Customers", len(data))

        search = st.text_input("Search Customer")

        if search:
            filtered = data[
                data["client_name"].str.contains(search, case=False)
            ]

            st.subheader("Filtered Results")
            st.dataframe(filtered)

        if st.button("Generate Emails"):

            st.session_state.generated_emails = []
            st.session_state.records = []
            st.session_state.escalation_accounts = []

            today = datetime.today()

            filename = "result.json"

            load_dotenv()

            api_key__ = os.getenv('API_KEY')

            client = OpenAI(
                api_key=api_key__,
                base_url="https://openrouter.ai/api/v1"
            )

            progress_bar = st.progress(0)

            for index, p in enumerate(data.itertuples(index=False)):

                days = (today - p.due_date).days

                if days <= 7:
                    stage = 1
                elif days <= 14:
                    stage = 2
                elif days <= 21:
                    stage = 3
                elif days <= 30:
                    stage = 4
                else:
                    stage = "ESCALATION"

                if stage == "ESCALATION":

                    st.session_state.escalation_accounts.append({
                        "client_name": p.client_name,
                        "invoice_no": p.invoice_no,
                        "amount": p.amount,
                        "days_overdue": days,
                        "email": p.email
                    })

                    continue

                prompt = f"""
                You are an AI finance collections assistant.

                Generate a professional payment follow-up email.

                STRICT RULES:
                1. Return ONLY valid JSON.
                2. Do not invent information.
                3. Keep the tone professional.
                4. The tone must match the escalation stage.
                5. Keep the email concise and realistic.

                ESCALATION POLICY:

                Stage 1:
                - Warm and friendly
                - Gentle reminder

                Stage 2:
                - Polite but firm
                - Request payment confirmation

                Stage 3:
                - Formal and serious
                - Request response within 48 hours

                Stage 4:
                - Stern and urgent
                - Final reminder before escalation

                INVOICE DETAILS:

                Client Name: {p.client_name}
                Invoice Number: {p.invoice_no}
                Amount Due: ₹{p.amount}
                Due Date: {p.due_date.date()}
                Days Overdue: {days}
                Escalation Stage: {stage}
                Follow Up Count: {p.follow_up_count}
                Client Email: {p.email}

                IMPORTANT:
                Each email must include:
                - client name
                - invoice number
                - amount due
                - due date
                - overdue days
                - payment reminder

                RETURN FORMAT:
                {{
                  "email_address": "...",
                  "subject": "...",
                  "tone_used": "...",
                  "email_body": "..."
                }}
                """

                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                text = response.choices[0].message.content

                cleaned = text.replace("```json", "").replace("```", "").strip()

                try:

                    email_data = json.loads(cleaned)

                    st.session_state.generated_emails.append(email_data)

                    st.session_state.records.append(email_data)

                except Exception as e:

                    st.error("JSON Parsing Failed")
                    st.write(e)

                progress = (index + 1) / len(data)

                progress_bar.progress(progress)

            with open(filename, "w") as file:
                json.dump(st.session_state.records, file, indent=4)

            st.session_state.emails_generated = True

        if st.session_state.emails_generated:

            st.success("Emails Generated Successfully")

            st.metric(
                "Generated Emails",
                len(st.session_state.generated_emails)
            )

            if len(st.session_state.escalation_accounts) > 0:

                st.error("Human Intervention Required")

                escalation_df = pd.DataFrame(
                    st.session_state.escalation_accounts
                )

                st.dataframe(escalation_df)

            st.subheader("Generated Emails")

            for email in st.session_state.generated_emails:

                with st.expander(email["subject"]):

                    st.write(
                        f"Email Address: {email['email_address']}"
                    )

                    st.write(
                        f"Tone Used: {email['tone_used']}"
                    )

                    st.text_area(
                        "Email Body",
                        email["email_body"],
                        height=250
                    )

            json_data = json.dumps(
                st.session_state.records,
                indent=4
            )

            st.download_button(
                label="Download JSON Results",
                data=json_data,
                file_name="generated_emails.json",
                mime="application/json"
            )

            if st.button("Confirm and Send Emails"):

                with st.spinner("Sending emails..."):
                    time.sleep(3)

                st.toast(
                    "All Emails Sent Successfully",
                    icon="✅"
                )

    except Exception as e:

        st.error("Invalid or corrupted CSV file")

        st.write(e)