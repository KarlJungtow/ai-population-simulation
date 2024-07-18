**Usage:**

**num_persons** specifies how many people are to be generated. When set to zero, the program will use the existing population from 'persons_sample.xlsx'

**num_questions** specifies the number of questions. To test all questions, use questions_df.shape[0]

**attributes** are currently just a placeholder and should later be loaded in from an excel file. To create a population, attributes must follow the order of Salary (lower/upper bound), Age (lower/upper bound), Years of Education (lower/upper bound) and Country

Gender is assumed to be either male, female or non-binary
 
 
 

**Cost calculation:**

Prices are for the newest model without Batches. 
For 1 million prompt tokens, OpenAI charges 5$. For every million tokens that ChatGPT produces they charge 15$. This means, that the total price cannot be calculated beforehand. 
However, since the answers will probably stay short (yes, no, a percentage) the price can be estimated. 


When creating a population, ChatGPT is prompted 120 tokens and will output 10-15 tokens.
Creating the subject is around 85 tokens

One Headline is between 10-20 tokens (estimated 15) and the 3 questions are 90 tokens each. 

For the answers I estimated a maximum of 15 Tokens (~8 words) per answer. 

Calculating with a generated population of 1000 and 100 questions the price would be:

Request tokens and prices:      

    Creation of every person: 1000*(120+85)     = 205 000                    
    Prompting the questions: 1000*100*3*(15+90) = 31.5*10^6       
    Total                                       = 31.7*10^6                   
    Total price                                 = 158.50$ 
 
  Output tokens and prices:
  
    Creation of every person:   1000*15        = 15 000
    Prompting the questions:    1000*100*3*15  = 4.5*10^6
    Total                                      = 4.5*10^6
    Total price                                = 67.50$
  
  
  Total cost  = 226$                               
