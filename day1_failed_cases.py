import pprint
import json

def load_test_results(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: file not found - {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: invalid JSON format - {file_path}")
        return None
    
def classify_error(error_code):
    if error_code is None:
        return None       
    if 500 <= error_code < 600:
        return "server error"
    if 400 <= error_code < 500:
        return "client error"
    return None 
## 上面的 return None 是處理「真的沒有值」；最下面的 return None 是處理「有值，但不符合任何分類」

def analyze_test_results(test_results):
    final_result = []
    required_fields = ["name", "status", "response_time"]

    for result in test_results:
        missing_required_field = False

        for field in required_fields:
            if field not in result:
                print(f"Invalid test case: missing required field - {field}")
                missing_required_field = True

        if missing_required_field:
            continue

        reasons = []

        if result["status"] == "failed": 
            reasons.append("failed")
        if result["response_time"] > 2:
            reasons.append("slow response")

        error_type = classify_error(result.get("error_code")) ## 是在「使用這個判斷器」

        if error_type:
            reasons.append(error_type)

        if reasons:
            final_result.append({
                "name": result["name"],
                "reasons": reasons
            })

        # append：加進 list, e.g. reasons.append("failed")
        # join：把 list 裡的字串接起來, e.g.  ", ".join(reasons)

    return final_result

def summarize_results(result):
    failed_count = 0
    slow_count = 0
    client_error = 0
    server_error = 0
    for item in result:
        if "failed" in item["reasons"]:
            failed_count += 1
        if "slow response" in item["reasons"]:
            slow_count += 1
        if "client error" in item["reasons"]:
            client_error += 1
        if "server error" in item["reasons"]:
            server_error += 1
    return {
        "total_abnormal": len(result),
        "failed": failed_count,
        "slow_response": slow_count,
        "client_error": client_error,
        "server_error": server_error
    }

def save_report(report, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    test_results = load_test_results("test_results.json")

    if test_results is None:
        print("Program stopped.")
    else:
        result = analyze_test_results(test_results)
        summary = summarize_results(result)

        report = {
            "summary": summary,
            "details": result
        }

        pprint.pprint(report)
        save_report(report, "analysis_report.json")

        print("Analysis report generated successfully.")
