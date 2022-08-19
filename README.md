# Spanish tourism market

## Tourist Hotspots and tourist expenditure

## 📌 Why this project?

Tourism is one of the main drivers of the Spanish economy and, like many other industries in the world, got hit during the COVID pandemic. To have a clearly idea of how much money moves around this market, I have decided to create two dashboards from Instituto Nacional de Estadística (INE) data:

- **Hotels and apartments dashboard.** Choose between more than 100 hotspots in Spain and observe how the hotel and touristic apartments demand and offer evolved from 2017 to mid-2022 (last data available). The metrics included are:
    - Overnight stays
    - Beds available
    - % of beds occupied
    - IPAP (Touristic Apartment Prices Index)
- Note: I wanted to include hotel price data (Average Daily Rate) for hotspots in this dashboard, but the only data available from INE was from 2021 to mid-2022.

- **Tourist expenditure profile dashboard.** We are a country of “sol y playa” (sun and beach tourism), but is this the main reason tourists visit Spain? I had many questions about the Spanish tourism quality and the expenditure of the visitors… Where do they tend to stay? Which countries spend the most in Spain? And how is this money distributed between CCAA? The answer to these questions can be found in this dashboard.

## 📌 Why this project?

Tourism is one of the main drivers of the Spanish economy and, as many other industries in the world, got hit hard during the COVID pandemic. In order to have a more clear idea of how many money moves this market and how it is distributed, I have decided to create two dashboards from Instituto Nacional de Estadística (INE) data:

- **Hotels and apartments dashboard.** Choose between more than 100 hotspots in Spain and observe how has the hotel and touristic apartments demand and offer evolved from 2017 to mid 2022 (last data available). The metrics included are:
    - Overnight stays
    - Beds available
    - % of beds occupied
    - IPAP (Touristic Apartment Prices Index)
    
    Note: I wanted to include hotel prices data (Average Daily Rate) for hotspots in this dashboard, but the only data available from INE was from 2021 to mid 2022. 
    
- **Tourist expenditure profile dashboard.** We are a country of “sol y playa” (sun and beach tourism), but is this the main reason tourists visit Spain? I had many questions about the Spanish tourism quality and the expenditure of the visitors… Where do they tend to stay? Which countries spend the most in Spain? And how is this money distributed between CCAA? The answer to these questions can be found in this dashboard.

## 👩🏼‍💻 How did I do it?

---

One of the main challenges I encountered during this project was deciding how many datasets should I use to build a proper dashboard. Turns out INE has a huge database of tourism data, but it is divided into smaller datasets that, are the same time, are divided by multiple categories. It was not an easy decision, but I finally decided to retrieve data from 16 datasets following these criteria:

- For the hotels and apartments dashboard, I used data filtered by tourist hotspots.
- For the tourist expenditure profile, I retrieved data with barely any level of detail.

The process:

### 1. INE API requests 📝

I created a function to retrieve data from the INE API in JSON format. First challenge: some of the data I gathered didn’t coincide with the data displayed on the web page or, on some occasions, the petition did not correspond to what I retrieved.

### 2. Cleaning data and EDA with Pandas 🔎

As I had decided to get smaller datasets from INE, it was not necessary to clean the numeric data. The missing values level was relatively low and I as was comparing temporary series, I decided to impute the missing values with 0.

The most challenging part was cleaning the categorical data. When you retrieve data from INE in JSON format, you’ll get a list of nested dictionaries with lots of information you can discard, but you will also get most of the key categorical data in one column and string format. Therefore, it is necessary to look closely at the unique values of each dataset to separate correctly the data. Also, it was important to be careful with the hotspots' names, as they were not harmonized.

Also, there were a lot of estimations, so it would be wise to keep updating the databases to obtain definite data in the following months.

### 3. **Visualization in Tableau 💻**

The next step of the process was to create the dashboards in Tableau. On the upper side of each dashboard, you’ll find a year selector, so you can compare the data annually. I invite you to check and play with the dashboards in my Tableau Public profile.

## 🚀Key takeaways

---

- Although the Spanish tourism market took a toll due to the COVID-19 pandemic, recent data seems to indicate that we are on the recovery path.
- The tourist apartments' beds offer has decreased since 2017. It would be interesting to explore the impact of the tourist property regulation on this matter.
- Stationarity can be seen clearly when looking at the demand-offer relationship. Overall, the percentage of beds occupied doesn’t exceed 50%.
- It is interesting to observe how the prices for the touristic apartments handled by tour operators have increased over the total prices. The price of apartments with more capacity (4/6) also rose over the general rate.
- Sun and beach tourism is our best attractive as a country, but there is also a clear interest in our cultural offer.
- Cataluña, the Balearic Islands, and the Canary Islands concentrate more than 50% of the tourist expenditure.
- Visitors from the Nordic Countries are the most interesting profile in terms of expenditure. It could be interesting to explore this way in a more detailed way.

## 📈Data sources

You can find the raw data and clean data in my GitHub repository. If you are interested in exploring the original data source, take a look at the statistics:

- Gasto de los turistas internacionales según comunidad autónoma de destino principal y país de residencia. Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=24746&L=0](https://www.ine.es/jaxiT3/Tabla.htm?t=24746&L=0)
- Gasto de los turistas internacionales según partidas de gasto y comunidad autónoma de destino principal. Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=24745](https://www.ine.es/jaxiT3/Tabla.htm?t=24745)
- Gasto de los turistas internacionales según tipo de alojamiento principal. Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=10836](https://www.ine.es/jaxiT3/Tabla.htm?t=10836)
- Gasto de los turistas internacionales según motivo principal del viaje. Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=10840](https://www.ine.es/jaxiT3/Tabla.htm?t=10840)
- Apartamentos. Viajeros y pernoctaciones por puntos turísticos. Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=2082&L=0](https://www.ine.es/jaxiT3/Tabla.htm?t=2082&L=0)
- Apartamentos. Plazas, apartamentos, grados de ocupación y personal empleado por puntos turísticos
Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=2022](https://www.ine.es/jaxiT3/Tabla.htm?t=2022)
- Índice de precios de apartamentos (IPAP): índice general nacional y desglose por modalidades
Source: [https://www.ine.es/jaxiT3/Datos.htm?t=2050](https://www.ine.es/jaxiT3/Datos.htm?t=2050)
- Índice de precios de apartamentos (IPAP): índice general nacional y desglose por tarifas
Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=2050&L=0](https://www.ine.es/jaxiT3/Tabla.htm?t=2050&L=0)
- Hoteles. Viajes y pernoctaciones por puntos turísticos. Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=2078](https://www.ine.es/jaxiT3/Tabla.htm?t=2078)
- Establecimientos, plazas estimadas, grados de ocupación y personal empleado por puntos turísticos. Source: [https://www.ine.es/jaxiT3/Tabla.htm?t=2066](https://www.ine.es/jaxiT3/Tabla.htm?t=2066)