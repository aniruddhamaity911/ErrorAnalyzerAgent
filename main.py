from services import extract_error_logs
from services import VectorStore
LOG_FILE_PATH = "D:\\DataEngineer\\trace-insight\\ErrorAnalyzerAgent\\resources\\enterprise-payment-service.log"
if __name__ == "__main__":
    print("starting")
    vector_store = VectorStore()
    errors = extract_error_logs(LOG_FILE_PATH)
    vector_store.save_errors(errors[:4])
    print("saving completed")
