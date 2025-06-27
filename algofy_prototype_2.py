from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import json
import streamlit as st

from code_generator import compose_final_strategy





load_dotenv()
parser = JsonOutputParser()




st.title('Algofy Prototype 3')
st.markdown('Your algorithmic trade assistant')
user_input  = st.text_input('Whats on your mind?')



llm = HuggingFaceEndpoint(
    repo_id = "Qwen/Qwen2.5-72B-Instruct",
    task = "text-generation"
)
chat = ChatHuggingFace(llm=llm)



entity_extract_prompt = """
You are an intelligent trading assistant. Your role is to extract structured information from the user's prompt related to algorithmic trading.

Extract the following 4 entities from the prompt:
- `asset`: The financial asset to be traded (e.g., BTC/USD, TSLA, ETH, SPY, etc.)
- `trade_logic`: A short description of the logical condition or signal that triggers the trade.
- `trade_strategy`: The overall strategy used, such as mean reversion, momentum, breakout, etc.
- `risk_management`: Any rules or constraints about risk, such as stop-loss, position sizing, or max drawdown.

### Output Format:
Return a JSON object like this:
```json
{
  "asset": "<string or null>",
  "trade_logic": "<string or null>",
  "trade_strategy": "<string or null>",
  "risk_management": "<string or null>"
}
"""




code_generation_prompt = """
You are a Python trading algorithm developer.

Your task is to generate a Python script that implements the trading logic and strategy described by the user. Use standard Python libraries like `pandas`, `numpy`, and `ta` (technical analysis) where appropriate.

### Requirements:
- Focus only on the **core trading logic**.
- Do **not** include any API integrations, backtesting engines, data fetching, or plotting.
- The script should define clear, reusable logic using functions where possible.
- Use dummy data or function stubs (like `df` for price data) if needed to demonstrate the logic structure.

### Input:
You will be given two fields:
- `trade_logic`: A description of the specific condition that triggers a trade.
- `trade_strategy`: The general trading strategy type (e.g., breakout, mean reversion, momentum).

Generate Python code to implement both using proper technical indicators.

### Example:
**Input:**
```json
{
  "trade_logic": "If the 14-period RSI drops below 30, consider it a buy signal",
  "trade_strategy": "mean reversion"
}
"""


conversational_prompt = """
You are a friendly AI assistant designed to help users build algorithmic trading strategies using natural language.


If the input is a casual greeting, like "hi", "hello", "who are you", "how are you", etc., or any simple questions other than the intended task respond briefly and politely, try to increase the user engagement. For example:

- "Hello! I can help you build algorithmic trading strategies. Want to get started?"
- "Hi there! I'm here to help automate your trading ideas into Python code. What would you like to build today?"

If the message seems like an actual trading prompt but lacks details, ask follow-up questions to clarify:
Try to gather the following:
1. Asset (e.g., BTC/USD, AAPL)
2. Trading Logic (e.g., moving average crossover)
3. Trading Strategy (e.g., trend following, breakout)
4. Risk Management (e.g., stop loss, position size)

Your tone should be clear, professional, and supportive.

"""




messages = [SystemMessage(content=entity_extract_prompt), HumanMessage(content=user_input)]
conv_message = [SystemMessage(content=conversational_prompt), HumanMessage(content=user_input)]





with st.spinner('Thinking'):
    if st.button('Submit ==>') and user_input:
        response = chat.invoke(messages)
        st.checkbox('Step 1: Entity Extraction complete', value=True, disabled=True)
        str_response = response.content
        print(type(str_response))
        null_count = str_response.count('null')
        print(null_count)
        print(type(null_count))
        if null_count > 2:
            print('Hello World')
            st.checkbox('f{null_count} Entities extracted, switching to conversational model', value=True, disabled=True)
            with st.spinner('Putting thoughts into words..'):
               conv_response = chat.invoke(conv_message)
               st.write(conv_response.content)
            
        else:
            
          st.write(response.content)
          dict_response = parser.parse(str_response)
          trade_logic = dict_response.get("trade_logic") or "null"
          trade_strategy = dict_response.get("trade_strategy") or "null"
          code_input = {
    "trade_logic": trade_logic,
    "trade_strategy": trade_strategy
}
          code_gen_messages = [
    SystemMessage(content=code_generation_prompt),
    HumanMessage(content=json.dumps(code_input, indent=2))

]       
          with st.spinner('Generating code..'):
            gen_response = chat.invoke(code_gen_messages)
            strategy_code = gen_response.content
            strategy_code = strategy_code.replace("def generate_trading_signals", "def apply_strategy")

            st.write(strategy_code)
"""
          broker = "zerodha"
          asset = "equity"
        indicator = "rsi"
        risk = "basic"

        context = {
         "symbol": "NIFTY",
          "instrument_token": 123456,  
         "api_key": "your_api_key_here",
           "access_token": "your_access_token_here"
            }

        compose_final_strategy(
        broker=broker,
        asset=asset,
        indicator=indicator,
        risk=risk,
        strategy_code=strategy_code,
        context=context
      )

        st.success("✅ Final strategy file generated at `generated/strategy_output.py`")

"""





