\# SmartToolAgent — 15 Test Questions



\*\*Purpose:\*\* Evaluate tool selection, tool execution, multi-tool handling, and final response generation.



| # | Question | Expected Tool | Actual Tools Used | Pass/Fail |

|---:|---|---|---|---|

| 1 | What is 25 multiplied by 16? | `calculator` | Pending test | Pending |

| 2 | Calculate 144 divided by 12. | `calculator` | Pending test | Pending |

| 3 | What is 2 raised to the power of 10? | `calculator` | Pending test | Pending |

| 4 | Calculate 75 + 125 - 50. | `calculator` | Pending test | Pending |

| 5 | What is 15% of 240? | `calculator` | Pending test | Pending |

| 6 | What is the current weather at latitude 24.8607 and longitude 67.0011? | `get\_weather` | Pending test | Pending |

| 7 | Get the current weather at latitude 31.5204 and longitude 74.3587. | `get\_weather` | Pending test | Pending |

| 8 | What is the weather at latitude 33.6844 and longitude 73.0479? | `get\_weather` | Pending test | Pending |

| 9 | Save a note saying I need to study tool calling. | `add\_note` | Pending test | Pending |

| 10 | Save a note saying complete the Week 1 README. | `add\_note` | Pending test | Pending |

| 11 | Show me my saved notes. | `list\_notes` | Pending test | Pending |

| 12 | What is 45 \* 12 + 30? | `calculator` | Pending test | Pending |

| 13 | Save a note saying test the agent loop, then show my notes. | `add\_note`, `list\_notes` | Pending test | Pending |

| 14 | Calculate 1000 / 25 and explain the result. | `calculator` | Pending test | Pending |

| 15 | What is the current weather at latitude 24.8607 and longitude 67.0011, and save a note saying check today's weather? | `get\_weather`, `add\_note` | Pending test | Pending |



\## Test Procedure



1\. Run each question through SmartToolAgent.

2\. Record the tool or tools actually called in \*\*Actual Tools Used\*\*.

3\. Mark \*\*Pass\*\* if the expected tool selection and execution succeed and the final answer is correct; otherwise mark \*\*Fail\*\*.

4\. For multi-tool questions, verify that both expected tools are called and the requested actions are completed.

5\. Weather tests depend on network access and the weather service; record service errors as test failures or blocked tests, as appropriate, and document the reason.



\## Test Summary



\- Total test cases: 15

\- Passed: Pending execution

\- Failed: Pending execution

\- Blocked by external services: Pending execution



\*\*Note:\*\* Results must be completed from actual test runs. Do not report unexecuted tests as passed.

