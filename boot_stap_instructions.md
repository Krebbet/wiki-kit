This wiki is intended to collect sources that will support a research project where I am trying to come up with a method to fine-tune small LLM models (1-40 Billion param) with a new techinque. Here are the requirements of the technique:

1. it must be able to learn concepts by specific examples, instead of learning through statistical inference. (ie. I want to be able to give it the experience of struggling with a problem or a concept and coming out the other side with a new understanding of something).
2. It should be able to use the same base problem or sample multiple times without overfitting
3. It should train on a single sample at a time.
4. The sample construction itself will be very important and I think there should be auxilliary information available for the LLM to call on that varies results over multiple tries.
5. The training should be concept based instead of sample and reward signal based (obviously there will be a singal that it is optimizing, but I mean we need to capture learning a concept somehow... not just getting closer to a goal pole.)
6. The method should require thinking, auxilliary choices and reward signals should capture getting components of the concept / signal correct.


Some Notes
- RL methods are a good place to start
- Anything that is thinking about data efficiency, close enough to this context is probably interesting.
- I expect Arxiv to have most of the sources we would be interested in.
- Figures and images are probably important here.
- Some Key concepts I think will be important to look for: Data Efficiency, Concept Learning, low sample size learning, exotic learning methods, Reinformcement Learning.
- Look for foundational papers in the fundamental topics and try to find some papers that link directly to this goal. From there use the references in those papers to further the research.
- It would be good to link wiki pages by reference and by concept (and anything else that you deem appropriate.)
