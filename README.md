# Chatbot_OPHELIA
This is a simple Python AI Chatbot with simulated emotions. She starts out not knowing much, but learns more from talking with you.

This chatbot starts with memory files that could be edited or replaced with files of your own choosing. 
As you talk to her, she learns new words marked under specific emotions, along with learning new replies from you, both of which update her memory.
In order to exit the conversation and allow saving of memory, simply enter "//exit" (Without the quotes). Else, the memory from that conversation
won't be saved. The conversation also outputs to 2 chatlog files. One is just the regular chat, while the extended chatlog (Xchatlog) contains
the conversations plus what OPHELIA is "thinking".

The only required outside program is espeak. If you choose to not use this feature, simply comment out line 100.

Update Version 0.01: OPHELIA now can recognize single terms from a user message, but only after OPHELIA has collected over 2000 words OPHELIA's emotion dictionary, and at least 500 learned reponses. Of course, if you choose to change this for your own purposes, it is easy, but it is recommended to only let that feature be activated after OPHELIA has learned a lot more. The reason is that if it is activated from the start, OPHELIA will not learn as many new responses, because terms from the user message will be detected instead, and will not activate her response learning code. Of course, this really opens the door for including even more, similar features, to be activated when OPHELIA learns even more.
