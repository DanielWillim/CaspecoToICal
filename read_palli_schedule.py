import pandas as pd
from datetime import datetime
from icalendar import Calendar, Event


def parse_timespan(date: str, timespan: str):
    start, end = timespan.split("-")
    if len(start) == 1:
        start = f"0{start}:00"
    start = datetime.strptime(f"{date} {start}", "%Y-%m-%d %H:%M")
    end = datetime.strptime(f"{date} {end}", "%Y-%m-%d %H:%M")
    return start, end


def parse_palli_schedule(file_path: str, out_path: str):
    df = pd.read_excel(file_path, sheet_name=None)

    calendar = Calendar()

    for sheet_name, sheet in df.items():
        print(sheet_name)
        print(sheet.head())
        relevant = sheet[["Unnamed: 1", "Palita"]]
        relevant.rename(columns={"Unnamed: 1": "date", "Palita": "working"}, inplace=True)
        print(relevant.head())
        for _, row in relevant.iterrows():
            date = row.date
            working = row.working
            if pd.isna(date) or pd.isna(working):
                continue
            date = date.strftime("%Y-%m-%d")

            print(date, working)
            if working == "L":
                continue

            start, end = parse_timespan(date, working)
            event = Event()
            event.add("summary", f"Jobb")
            event.add("dtstart", start)
            event.add("dtend", end)
            calendar.add_component(event)

    with open(out_path, "wb") as f:
        f.write(calendar.to_ical())


if __name__ == "__main__":
    parse_palli_schedule("/Users/willim/dev-private/CaspecoToICal/data/palli_schema_q4.xlsx", "/Users/willim/Downloads/calendar2.ics")
