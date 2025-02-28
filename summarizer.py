import tiktoken
from openai import OpenAI

class Summarizer:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.encoder = tiktoken.encoding_for_model("gpt-3.5-turbo") #which model should i use?
        self.token_limit =  4096 #Total tokens model has access to
        self.summary_buffer = 500 #Tokens reserved for AI response
    
    def count_tokens(self, history):
        """Count the total tokens in the conversation history."""
        tokens = 0
        for msg in history:
            # Safely retrieve content, defaulting to an empty string
            content = msg.get("content","")
            # Ensure content is a string 
            if isinstance(content, str):
                tokens += len(self.encoder.encode(content)) + 4 #Add message overhead
            else:
                # Issue a warning for non-string content
                print(f"Warning: Non-string content found in message. Type: {type(content)}")
                tokens += 4  # Add minimal overhead for invalid content

        return tokens


    def summarize_conversation(self, messages) :
        #join role and context into dict. 
        conversation_text = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in messages
        )

        response =  self.ai_client.chat.completions.create(
            model = "deepseek-chat",
            messages = [
                {"role": "system", "content": "You are Socrates. Summarize key discussion points."},
                {"role": "user", "content": f"Summarize this conversation for future reference:\n{conversation_text}"}
            ]
        )
        return response.choices[0].message.content
    


    def optimize_history(self, messages, session_summary):
        optimized = [
            {"role": "system", "content": session_summary}
        ]
        tokens_used = self.count_tokens(optimized)

        #Add most recent messages until token limit is reached
        for msg in reversed(messages): #why reversed?
            msg_tokens = len(self.encoder.encode(msg["content"])) + 4

            if tokens_used + msg_tokens <= self.token_limit-self.summary_buffer:
                optimized.insert(1, msg)
                tokens_used + msg_tokens
            else:
                break
        
        return optimized
    
    #If you still want to summarize earlier, add multiple thresholds:

    # def should_summarize(self, messages):
    #     token_count = self.count_tokens(messages)
        
    #     # Tiered thresholds
    #     if token_count > 3000:  # 75% of 4096
    #         return True
    #     elif token_count > 2000 and len(messages) > 10:
    #         return True  # Summarize long but low-token conversations
    #     return False

    
