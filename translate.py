import jsonlines

TABLES = "data/dev.tables.jsonl"
QUERIES = "data/dev.jsonl"
PREDICTIONS = "test/my.pred.dev.jsonl"

tables = {}

# Read tables and data
with jsonlines.open(TABLES) as input_tables:
    for table in input_tables:
        tables[table["id"]] = table

# Open queries and output file
with jsonlines.open(QUERIES) as input_queries, jsonlines.open(PREDICTIONS, mode='w') as predictions_file:
    for query in input_queries:
        question = query["question"].lower()
        table = tables[query["table_id"]]

        # Determine selection
        sel = -1
        for i, field in enumerate(table["header"]):
            if field.lower() in question:
                sel = i

        # Determine conditions
        conds = []
        for row in table["rows"]:
            for i, cell in enumerate(row):
                if isinstance(cell, str):
                    if cell.lower() in question:
                        conds.append([i, 0, cell])

        prediction = {"query": {"sel": sel, "conds": conds, "agg": 0}, "error": ""}
        predictions_file.write(prediction)
