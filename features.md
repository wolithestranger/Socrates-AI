# 1.0 Schedule

# 2.0 Timer

# 3.0 Socrates AI
    #3.1 Prompt Engineering
        #3.1.1 Uses Socratic method to teach, when in study mode.
        #3.1.2 Uses 80/20 method. i.e the most important 20% that will help me understand 80% of the content. 
        #3.1.3 If need be it will use metaphors and stories to aid my memory
        #3.1.4 Could create roadmaps 
        #3.1.5 Will remind of projects that are not yet finished, to avoid having a backlog of projects that are incomplete.

# 4.0 OpenCV package to take in images
    contrast the image so more visible
    Tesseract with image_to_string function 
    Image is then fed into LLM, with an awaiting prompt to complete a certain instruction.

**DONE**
    * Summarization of prompts added and Session Manager done. the LLM gives a short summary of what was discussed. Saves tokens. Session Manager done. Session details are saved in a json file, each session with a timestamp (datetime.now()) and then summarized. The two go hand in hand. Summarization is done automatically when 75% of token limit is reached. 

    75% because, each summarization call costs tokens/ money and adds latency. Summarizing a 100 token convo wastes API calls for no reason. 
    Also, if the summaries are too basic, then over-summarizing could affect and skew the responses.  *important*

    This implies there is a token Buffer of 25%, reserving space for new user questions, AI responses, system messages.

    Its also more natural if there are about 10-15 exchanges before summarizing. 
    Short convos dont need summarizing, unless details are important, in which case i can just tell it to save. Long convos get summarized only when necessary.  

    MAX OF 4096 TOKENS PER REQUEST. What exactly is a request? it is a session ---
    Each API request includes the entire conversation history up to that point, so the token limit applies per request. If the accumulated tokens (system message + history + new question + response) exceed the model's limit, the request will fail. The 75% threshold is a precaution to start summarizing before hitting the limit.




    this currently reduces token usage by like 60% - 80% 

    Maybe next, it would be worth it to try embedding(instead of TF-DIF). 


***TO DO**

# 1.0 Combine all the features 
    Later on, find a way to add all the features into one. I.E you can just enter a command to enter "add go to gym at 8pm to my schedule" or "turn on study mode. To do this, it would be preferable if the response time is faster. 

# 2.0 Give Socrates Memory
    If Socrates has memory I can continue building Socrates with Socrates. It would be fulfilling it's purpose
    Potential ways to enhance memory.
    * Token optimization - Only the relevant tokens are requested within each api request. 
    * TF-DIF - Instead of using this use embedding instead. Capture the semantic meaning instead, e.g "gravity" ~ "relativity". 
    * Summarization - Prioritize context, without saving the entire convo becasue this will save tokens.  Its an artificial brain, it will connect dots, because it has the underlying. Our brains do this too.
    * Session based storage - All the data from the session is grouped, perhaps for efficiency. This could be paired with the summarization technique and there could be a summarization for the whole session. 
    * Database - Using an unstructured database, e.g postSql or Mongo or Cassandra. What are the benefits to doing this? What is the difference if the tokesn are being counted from another place?
    * Layered Storage - Not all data is stored the same way. Data like my progress and my identity could be stored in a faster, more expensve form of data storage, in this case like my hard drive, while less frequently accessed data, like conversation data could be stored in the database or something. 

    Check the efficiency of each one by comparing to the efficiency of the prior method 

    Efficiency of Summarization - 50% - 80% 

    Summarization reduces tokens used per request, however increases processing time. The thng is already slow.
    

# 3.0 Give Socrates access to files in this directory
    This will allow it to see and keep track of files in directory as needed. It will not make any changes to the files (no idea how it would even do that). It should have access as this will make it easy to reference files when building projects. Maybe to start, it will be able to read files and later  on be able to write to different files and access different folders. Later on, it might have access to certain folders within the computer. 

# 4.0 Give Socrates the ability to browse the web and commplete    certain web related tasks. 

# 5.0 Some form of basic UI will be needed soon
    So that formulas can be displayed etc.

    #4.1 Image submission will  important as well. 

# 6.0 Give Socrates Access to the date and time. So he has some perception of time. Shouldn't be too hard.  


# Potential Features
    *Encryption. Would it be wise to make the encryptions end to end? Would i want to have access to the users requests? It might be a good idea and they can use it to search hpotentially harmful things. At the same time the user has a right to their full privacy. Perhaps some holds on the degrees of freedom the AI is allowed to give the user access to, e.g no harmful content. This goes outside the bounds of encryption but is still useful to think about.  