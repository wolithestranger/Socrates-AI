# Scheduler



# Cycle and Time returns

Is there a way to use threading, or make it so that every time you 
send a command, it lets you know how many minutes are left in the session?
Later on, there will be a visible timer.

# API calls take forever. 
Why is this happeneing? i paid for the api. should i not get some 
form of priority?
is it the way im doing the calls?
How do i make it faster?

Time the API calls


# The chat Memory
Currently, the AI's memory isnt handled very efficiently. 
It stores teh last 10 messages. if no of messages is greater than 
max messages, last one/ oldest one s popped. 
This is an attempt to minimize token usage to maintain the limit 

It is stored in a list of dictionaries like so


def _ask_ai(self, question):
    try:
        # Append user's question to history
        self.conversation_history.append({"role": "user", "content": question})

        # Trim history to avoid token limits (keep last 6 exchanges)
        max_history_length = 12  # 6 user + 6 assistant messages (plus system message)
        if len(self.conversation_history) > max_history_length + 1:
            # Remove oldest messages but keep the system message
            self.conversation_history = [
                self.conversation_history[0]  # Keep system message
            ] + self.conversation_history[-max_history_length:]

        # Send full history to API
        response = self.ai_client.chat.completions.create(
            model="deepseek-chat",
            messages=self.conversation_history,
            stream=False
        )

        # Store AI's response in history
        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})

        return ai_response
    except Exception as e:
        return f"Error: {str(e)}"



i need a more evvicient way to handle this.

do i just clear the history myself? 4096 tokens is not a lot tbh


Advanced Improvements (Optional)
Token Counting: Use libraries like tiktoken to precisely track token usage.

Long-Term Storage: Save history to a file/database for cross-session memory.

Summary Messages: Periodically summarize old conversations to preserve context.

could use TF-DIF
**Term Frequency-Inverse Document Frequency**


Manybe some type or persistent memory system. like a database maybe 
