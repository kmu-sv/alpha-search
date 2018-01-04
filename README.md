# Alpha Search
## Authors 
*Minjun Koo, Gaeul Go, Hwancheol Kang, Kihyun Yang*<br>
*- Kookmin University Computer Science*

## Overview

Alpha-Search is a chatbot-style recommendation system for users who are looking for multiple cafes for users who are looking for coffee shops where they can bring their laptop to do things. If a user asks chatbot to find a cafe that has user wants (e.g. Table shape , WiFi, Enough of a lot of outlet(number of outlets / number of seats > t : t is an arbitrary number to be determined later), etc.), Chatbot will give you a couple of candidates on the map based on the data stored in the DB . When users click on a candidate provided with a pin on map, detailed information about the place is provided and the user makes a decision among the candidates based on this information. Then, the chatbot provides a route to the selected location. In addition, the chatbot asks the user what they may need in addition to what the user has requested and use this information to determine the candidates.

## Flowchart

![flowchart](./flow_chart.png)

## Infrastructure
Server Infra : AWS EC2<br>
DB : MariaDB<br>
MariaDB 10.3.3<br>
Rule : (blank)<br>
Table : User, Place<br>
version management : github<br>

## Feature 1. Enter User Question
## Feature 2. Chat
## Feature 3. Show suggested places

