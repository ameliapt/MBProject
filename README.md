# Spanish tourism market

An analysis of tourist hotspots, hotel and apartments market and tourist expenditure.

## 📌 Why this project?

Tourism is one of the main drivers of the Spanish economy and, like many other industries in the world, got hit during the COVID pandemic. To understand how money moves around this market, I have created two dashboards using data from Instituto Nacional de Estadística (INE):

- **Hotels and apartments dashboard.** Choose between more than 100 hotspots in Spain and observe how the hotel and touristic apartments demand and offer evolved from 2017 to mid-2022 (last data available). The metrics included are:
    - Overnight stays
    - Beds available
    - % of beds occupied
    - IPAP (Touristic Apartment Prices Index)
- Note: I didn’t include hotel price data (Average Daily Rate) for hotspots in this dashboard because there was only data for the last 12 months.

- **Tourist expenditure profile dashboard.** We are a country of “sol y playa” (sun and beach tourism), but is this the main reason tourists visit Spain? I had many questions about the Spanish tourism quality and the expenditure of the visitors… Where do they tend to stay? Which countries spend the most in Spain? And how is this money distributed between CCAA? The answer to these questions can be found in this dashboard.

## 👩🏼‍💻 How did I do it?

One of the main challenges I encountered during this project was deciding how many datasets I should use to build a proper dashboard. It turns out INE has a huge database of tourism data which is composed of multiple smaller datasets. I selected 16 datasets following these criteria:

- For the hotels and apartments dashboard, I selected datasets where data can be segmented by tourist hotspots.
- For the tourist expenditure profile, I retrieved data at country level.

The process:

### 1. INE API requests 📝

I created a function to retrieve data from the INE API in JSON format. First challenge: some of the data I gathered didn’t coincide with the data displayed on the web page or sometimes the retrieved data did not correspond to what I requested.

### 2. Cleaning data and EDA with Pandas 🔎

As I had decided to get smaller datasets from INE, it was not necessary to clean the numerical data. The missing values rate was relatively low and as I was comparing temporary series, I decided to impute the missing values with 0.

The most challenging part was cleaning the categorical data. When you retrieve data from INE in JSON format, you’ll get a list of nested dictionaries with lots of information you can discard, but you will also get most of the key categorical data in one column and string format. Therefore, it is necessary to look closely at the unique values of each dataset to separate the data correctly. Also, it was important to be careful with the hotspots' names, as they were not standarized.

Also, many data points were estimations, so it would be wise to keep updating the databases to obtain definite data in the following months.

### 3. **Visualization in Tableau 💻**

The next step of the process was to create the dashboards in Tableau. On the upper side of each dashboard, you’ll find a year selector, so you can compare the data annually. I invite you to check and play with the dashboards in my Tableau Public profile.

## 🚀Key takeaways

- Although the Spanish tourism market took a toll due to the COVID-19 pandemic, recent data seems to indicate that we are on the recovery path.
- The tourist apartments' beds offer has decreased since 2017. It would be interesting to explore the impact of the tourist property regulation on this matter.
- Seasonality can be clearly seen when looking at the demand-offer relationship. Overall, the percentage of beds occupied doesn’t exceed 50%.
- It is interesting to observe how the prices for the touristic apartments handled by tour operators have increased signifcantly more than normal and weekend prices. The price of apartments with capacity of 4 to 6 people increased more than smaller apartments/studios, which may mean than there is now more demand for spacious apartments or less supply (as we saw total appartment supply decrease).
- Sun and beach tourism the main reason to visit our country, but there is also a clear interest in our cultural offer.
- Cataluña, the Balearic Islands, and the Canary Islands receives more than 50% of the tourist expenditure.
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