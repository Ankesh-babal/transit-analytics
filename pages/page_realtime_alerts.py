{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "fbc19e41-6ee2-46db-a090-f1a23e0553bc",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-05-03 21:00:21.353 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'utils.realtime'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[2], line 3\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mstreamlit\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mst\u001b[39;00m\n\u001b[0;32m      2\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mstreamlit_autorefresh\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m st_autorefresh\n\u001b[1;32m----> 3\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mutils\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mrealtime\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m get_realtime_data\n\u001b[0;32m      4\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mutils\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01malerts\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m generate_alerts\n\u001b[0;32m      6\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21mshow\u001b[39m():\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'utils.realtime'"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "from streamlit_autorefresh import st_autorefresh\n",
    "from utils.realtime import get_realtime_data\n",
    "from utils.alerts import generate_alerts\n",
    "\n",
    "def show():\n",
    "    st.title(\"🚨 Real-Time Alerts\")\n",
    "\n",
    "    st_autorefresh(interval=30_000, key=\"alerts_refresh\")\n",
    "\n",
    "    df_rt = get_realtime_data()\n",
    "\n",
    "    st.subheader(\"Live Feed (Last 20 Records)\")\n",
    "    st.dataframe(df_rt)\n",
    "\n",
    "    alerts = generate_alerts(df_rt)\n",
    "\n",
    "    st.subheader(\"Active Alerts\")\n",
    "\n",
    "    if alerts.empty:\n",
    "        st.success(\"No active alerts. System stable.\")\n",
    "    else:\n",
    "        for _, row in alerts.iterrows():\n",
    "            if row[\"severity\"] == \"HIGH\":\n",
    "                st.error(f\"[{row['route']}] {row['message']}\")\n",
    "            elif row[\"severity\"] == \"MEDIUM\":\n",
    "                st.warning(f\"[{row['route']}] {row['message']}\")\n",
    "            else:\n",
    "                st.info(f\"[{row['route']}] {row['message']}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "a07e8248-98eb-4168-b7e4-9e5d0d95e544",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "ERROR: Could not find a version that satisfies the requirement utils.realtime (from versions: none)\n",
      "\n",
      "[notice] A new release of pip is available: 26.0.1 -> 26.1\n",
      "[notice] To update, run: python.exe -m pip install --upgrade pip\n",
      "ERROR: No matching distribution found for utils.realtime\n"
     ]
    }
   ],
   "source": [
    "pip install utils.realtime\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b1ddbf44-a3f5-4910-9132-6603b4d5dc02",
   "metadata": {},
   "outputs": [],
   "source": []
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
