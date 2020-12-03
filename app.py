import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)

# Flask Routes
#################################################
#  List all routes that are available

@app.route("/")
def welcome ():
    # List all available api routes
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start/end<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    #   Query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
              order_by(Measurement.date).all()
    # convert results list to list of dictionaries
    results_dict = []

    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        results_dict.append(new_dict)

    session.close()

    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # return a JSON list of stations from the dataset.
    results = session.query(Station.station).all()

    # Convert array into normal list
    stations = list(np.ravel(results))

    session.close()

    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Get the date from one year ago
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the dates and temperature observations of the most active station for the last year of data. 
    results = session.query(Measurement.tobs).\
              filter(Measurement.station == 'USC00519281').\
              filter(Measurement.date >= prev_year).all()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    # convert array into normal list
    temps = list(np.ravel(results))

    session.close()

    return jsonify(temps=temps)

@app.route("/api/v1.0/start")
@app.route("api/v1.0/start/end")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

#   Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

if __name__ == '__main__':
    app.run(debug=True)








