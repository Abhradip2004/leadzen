from app.db import create_lead

lead = create_lead(
    "your_institute_id_here",
    "9876543210",
    "What is the fee structure?"
)

print(lead)