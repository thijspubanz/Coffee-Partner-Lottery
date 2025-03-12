# CaféConnect
A social application for generating random pairings of people who can connect over a virtual chat and coffee together. The Python script in this repo takes care of the generation, my whole process for the lottery is as follows: 

1. Let interested people sign up. I use MS Forms for the Coffee Partner Lottery at UU's Department of Information and Computing Sciences (template available [here](https://forms.office.com/Pages/ShareFormPage.aspx?id=oFgn10akD06gqkv5WkoQ51EXCAYj7jZCpuwTHAmfcRhUQk1ZOEtTTDJBQVozU0tVN0ZSNlFGWDEwNC4u&sharetoken=NNfcIwyZoQl07ZdXpHkZ)), but Google Forms or another similar tool will also do. You can download the responses and save them as a CSV file (recommended name "Coffee Partner Lottery participants.csv"), which is the input for the Python script.  
2. Run the Python script to generate a set of pairs. It will store all pairs ever generated in another CSV file ("Coffee Partner Lottery all pairs.csv"), to keep track of already generated pairs and thus making sure that new people meet each time. The new set of pairs is written to a separate CSV file ("Coffee Partner Lottery new pairs.csv"). 
3. Use Thunderbird's MailMerge plugin to automatically generate e-mails with the information from "Coffee Partner Lottery new pairs.csv", to inform people that they have been paired. I haven't tried, but probably MS Outlook and other e-mail clients have similar functionality. Alternatively, you can just copy the list of pairs from the program output or from the file "Coffee Partner Lottery new pairs.txt" and send them to a Teams chat, group mailing list, or similar.

# Other Versions
Different people have implemented variations of the same idea. Some that I am aware of: 
* [Et9797's extension](https://github.com/Et9797/mysterycoffee), written in Python and using Google services for participant signup and e-mail notifications 
* Barbara Vreede's [Mystery Coffee](https://github.com/bvreede/mystery_coffee), written in R
