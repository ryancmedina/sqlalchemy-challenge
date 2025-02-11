# Import the dependencies.
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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    date_lim = "2016-08-23"

    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(measurement.prcp, measurement.date).filter(measurement.date >= date_lim)

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    prec_df = pd.DataFrame(precipitation)

    session.close()

    prec_df = prec_df.dropna()
    prec_df = prec_df.sort_values("date")

    prec_dict = dict(zip(prec_df.date, prec_df.prcp))

    return jsonify(prec_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all station names
    results = session.query(station.name).all()

    session.close()

    # Convert results into list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    date_lim = "2016-08-23"

    # Query all temperatures after desired date
    tobs = session.query(measurement.date, measurement.tobs).filter(measurement.date >= date_lim).filter(measurement.station == "USC00519281")

    session.close()

    tobs_df = pd.DataFrame(tobs)

    # Convert results into list
    tobs_dict = dict(zip(tobs_df.date, tobs_df.tobs))

    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    date_lim = start

    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(measurement.tobs).filter(measurement.date >= date_lim)

    # Save the query results as a Pandas DataFrame
    prec_df = pd.DataFrame(precipitation)

    session.close()

    prec_df = prec_df.dropna()
    
    # Comvert results into dictionary
    prec_dict = {
        "Minimum Temperature" : prec_df["tobs"].min(),
        "Maximum Temperature" : prec_df["tobs"].max(),
        "Average Temperature" : prec_df["tobs"].mean(),
    }

    return jsonify(prec_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    date_lim = start
    date_max = end
    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(measurement.tobs).filter(measurement.date >= date_lim).filter(measurement.date <= date_max)

    # Save the query results as a Pandas DataFrame
    prec_df = pd.DataFrame(precipitation)

    session.close()

    prec_df = prec_df.dropna()
    
    # Comvert results into dictionary
    prec_dict = {
        "Minimum Temperature" : prec_df["tobs"].min(),
        "Maximum Temperature" : prec_df["tobs"].max(),
        "Average Temperature" : prec_df["tobs"].mean(),
    }

    return jsonify(prec_dict)

if __name__ == '__main__':
    app.run(debug=True)