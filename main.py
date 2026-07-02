from services import extract_error_logs
LOG_FILE_PATH = "D:\\DataEngineer\\trace-insight\\ErrorAnalyzerAgent\\resources\\enterprise-payment-service.log"
if __name__ == "__main__":

    print(extract_error_logs(LOG_FILE_PATH)[0])