{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "6c427bed-0412-4652-a870-828b5ef438a5",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "\n",
    "def get_realtime_data():\n",
    "    df = pd.read_csv(\"data/dummy_trip_updates.csv\")\n",
    "    df = df.sort_values(\"timestamp\").tail(20)   # last 20 events\n",
    "    return df\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
