# SmartToolAgent — 15 Test Questions

**Purpose:** Evaluate tool selection, tool execution, multi-tool handling, error handling, and final response generation.

## Test Cases

| # | Question | Expected Tool(s) | Actual Tools Used | Status |
|---:|---|---|---|---|
| 1 | What is 25 multiplied by 16? | `calculator` | Pending | Pending |
| 2 | Calculate 144 divided by 12. | `calculator` | Pending | Pending |
| 3 | What is 2 raised to the power of 10? | `calculator` | Pending | Pending |
| 4 | Calculate 75 + 125 - 50. | `calculator` | Pending | Pending |
| 5 | What is 15% of 240? | `calculator` | Pending | Pending |
| 6 | What is the current weather at latitude 24.8607 and longitude 67.0011? | `get_weather` | Pending | Pending |
| 7 | Get the current weather at latitude 31.5204 and longitude 74.3587. | `get_weather` | Pending | Pending |
| 8 | What is the weather at latitude 33.6844 and longitude 73.0479? | `get_weather` | Pending | Pending |
| 9 | Save a note saying I need to study tool calling. | `add_note` | Pending | Pending |
| 10 | Save a note saying complete the Week 1 README. | `add_note` | Pending | Pending |
| 11 | Show me my saved notes. | `list_notes` | Pending | Pending |
| 12 | What is 45 * 12 + 30? | `calculator` | Pending | Pending |
| 13 | Save a note saying test the agent loop, then show my notes. | `add_note`, `list_notes` | Pending | Pending |
| 14 | Calculate 1000 / 25 and explain the result. | `calculator` | Pending | Pending |
| 15 | What is the current weather at latitude 24.8607 and longitude 67.0011, and save a note saying check today's weather? | `get_weather`, `add_note` | Pending | Pending |

**Status values:** `Pass`, `Fail`, `Blocked`, or `Pending`.

## Test Procedure

1. Run each question through SmartToolAgent.
2. Record the actual tool names from the execution logs in **Actual Tools Used**.
3. Mark `Pass` only if the expected tool execution succeeds and the final answer is correct.
4. Mark `Fail` if the tool selection, execution, or final answer is incorrect.
5. Mark `Blocked` if an external dependency, such as the weather API, prevents the test from being completed. Record the reason.
6. For multi-tool tests, verify that all expected tools execute and the requested actions are completed.
7. Keep the same test inputs when repeating tests so results can be compared consistently.

## Test Summary

- **Total test cases:** 15
- **Passed:** Pending execution
- **Failed:** Pending execution
- **Blocked by external services:** Pending execution
- **Not yet executed:** 15

Update these totals after running the tests. Do not count pending or blocked tests as passed.

## Notes

- Weather tests require network access and a functioning weather service.
- Note-related tests may change the saved notes in the application's storage.
- Test results must reflect actual executions and observed outputs.
