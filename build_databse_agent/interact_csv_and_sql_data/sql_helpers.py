# Create two functions to have better control over the llm output
# The helper functions got access to all_states_history because: I created that table earlier with df.to_sql(...) and the functions query it through the same database engine which points to that same .db file.

import numpy as np
import pandas as pd
from sqlalchemy import text

def get_hospitalized_increase_for_state_on_date(engine, state_abbr, specific_date):
    try:
        query = text("""
        SELECT date, hospitalizedIncrease
        FROM all_states_history
        WHERE state = :state_abbr AND date = :specific_date
        """)

        with engine.connect() as connection:
            result = pd.read_sql_query(
                query, 
                connection, 
                params={
                    "state_abbr": state_abbr,
                    "specific_date": specific_date
            }
            )
        if not result.empty:
            return result.to_dict('records')[0]
        else:
            return np.nan
    except Exception as e:
        print(e)
        return np.nan


def get_positive_cases_for_state_on_date(engine, state_abbr, specific_date):
    try:
        query = text("""
        SELECT date, state, positiveIncrease AS positive_cases
        FROM all_states_history
        WHERE state = :state_abbr AND date = :specific_date
        """)

        with engine.connect() as connection:
            result = pd.read_sql_query(
                query, 
                connection,
                params={
                    "state_abbr": state_abbr,
                    "specific_date": specific_date
            }
            )
        if not result.empty:
            return result.to_dict('records')[0]
        else:
            return np.nan
    except Exception as e:
        print(e)
        return np.nan


tools_sql = [
    {
        "type": "function",
        "function": {
            "name": "get_hospitalized_increase_for_state_on_date",
            "description": """Retrieves the daily increase in
                              hospitalizations for a specific state
                              on a specific date.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": """The abbreviation of the state
                                          (e.g., 'NY', 'CA')."""
                    },
                    "specific_date": {
                        "type": "string",
                        "description": """The specific date for
                                          the query in 'YYYY-MM-DD'
                                          format."""
                    }
                },
                "required": ["state_abbr", "specific_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_positive_cases_for_state_on_date",
            "description": """Retrieves the daily increase in 
                              positive cases for a specific state
                              on a specific date.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": """The abbreviation of the 
                                          state (e.g., 'NY', 'CA')."""
                    },
                    "specific_date": {
                        "type": "string",
                        "description": """The specific date for the
                                          query in 'YYYY-MM-DD'
                                          format."""
                    }
                },
                "required": ["state_abbr", "specific_date"]
            }
        }
    }
]