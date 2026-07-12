from services import extract_error_logs
from services import VectorStore
LOG_FILE_PATH = "D:\\DataEngineer\\trace-insight\\ErrorAnalyzerAgent\\resources\\library_management_enterprise_5mb.log"
if __name__ == "__main__":
    print("starting")
    vector_store = VectorStore()
    errors = extract_error_logs(LOG_FILE_PATH)
    for e in errors:
        if "REQ-9011948" in e.raw_error:
            print(e)
    # vector_store.save_errors(errors)
    print("saving completed")
