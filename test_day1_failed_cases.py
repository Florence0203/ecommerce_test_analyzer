import pytest
from day1_failed_cases import classify_error, analyze_test_results, summarize_results


def test_analyze_normal_case():
    test_data = [
        {
            "name": "login_success",
            "status": "passed",
            "response_time": 0.8,
            "error_code": 200
        }
    ]
    result = analyze_test_results(test_data)
    assert result == []

def test_analyze_slow_response(sample_test_data):
    
    result = analyze_test_results(sample_test_data)
    assert result == [
        {
            "name": "checkout_coupon",
            "reasons": ["slow response"]
        }
    ]

def test_analyze_multiple_reason():
    test_data = [
    {
        "name": "payment_api",
        "status": "failed",
        "response_time": 4.2,
        "error_code": 400
    }
    ]
    result = analyze_test_results(test_data)
    assert result == [
            {
                "name": "payment_api",
                "reasons": [
                "failed",
                "slow response",
                "client error"
                ]
            }
        ]

def test_analyze_missing_required_failed():
    test_data = [
        {
            "name": "payment_api",
            "response_time": 4.2,
            "error_code": 503
        }
    ]

    result = analyze_test_results(test_data)

    assert result == []

def test_analyze_missing_required_field_message(capsys):
    test_data = [
    {
        "name": "payment_api",
        "response_time": 4.2,
        "error_code": 400
    }
    ]
    result = analyze_test_results(test_data)
    assert result == []

    captured = capsys.readouterr()

    assert "Invalid test case: missing required field - status" in captured.out

@pytest.mark.parametrize(
    "error_code, expected",
    [
        (404, "client error"),
        (503, "server error"),
        (200, None),
        (None, None)
    ]
)
def test_classify_error_parameterized(error_code, expected):
    assert classify_error(error_code) == expected


def test_summarize_results(abnormal_results):

    result = summarize_results(abnormal_results)

    assert result == {
            "total_abnormal" : 3,
            "failed" : 2,
            "slow_response" : 1,
            "client_error" : 1,
            "server_error" : 1
        }

@pytest.fixture
def sample_test_data():
    return[
        {
            "name": "checkout_coupon",
            "status": "passed",
            "response_time": 2.8,
            "error_code": 200
    }
    ]

@pytest.fixture ## fixture = 共用的測試 setup，不等於所有 test 一定用同一份資料
def abnormal_results():
    return[
            {
                "name": "case1",
                "reasons": ["failed"]
            },
            {
                "name": "case2",
                "reasons": ["slow response", "server error"]
            },
            {
                "name": "case3",
                "reasons": ["failed", "client error"]
            }
    ]