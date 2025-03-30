mkdir -p app/agents data
# Copy the PDF files to the data directory
cp *.pdf data/
# Create the Python files as described above
# Install dependencies
pip install -r requirements.txt
# Run the FastAPI application
python app/main.py