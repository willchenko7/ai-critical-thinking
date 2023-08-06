# ai-critical-thinking

For an ai to become truly intelligent, it needs to be able to think critically and solve problems that it was not trained on. Imo, large language models such as gpt, bert, or llama, are not well-suited for this task, because they are bascially trained on the entire corpus of human thought. How can we test if it can think critically and solve problems if there is nothing left to test it on?

In this repo, I aim to tackle this problem by strategically gathering training data, training an neural network on it, and giving it a test on somethine just out of it's reach. 

I think a good starting place for this are elementarty math textbooks. Math is a good starting place because it is the language of logic, and each topic is built on top of another. For example, if an intelligent system was trained to know about cartesian plots, and knew how to calculate the distance between two points, it should be able to calculate the length of a hypotenuse on a right trianglge, given the two other sides, without ever being explicity trained on the pythagorean theorem.