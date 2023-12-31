import csv
import json

csv_file_path = "final_dataset.csv"
json_file_path = "output.json"

def convert_csv_to_json():
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []

        for row in reader:
            data.append({
                "id": int(row["id"]),
                "Date": row["Date"],
                "HomeTeam": row["HomeTeam"],
                "AwayTeam": row["AwayTeam"],
                "FTHG": int(row["FTHG"]),
                "FTAG": int(row["FTAG"]),
                "FTR": row["FTR"],
                "HTGS": int(row["HTGS"]),
                "ATGS": int(row["ATGS"]),
                "HTGC": int(row["HTGC"]),
                "ATGC": int(row["ATGC"]),
                "HTP": float(row["HTP"]),
                "ATP": float(row["ATP"]),
                "HM1": row["HM1"],
                "HM2": row["HM2"],
                "HM3": row["HM3"],
                "HM4": row["HM4"],
                "HM5": row["HM5"],
                "AM1": row["AM1"],
                "AM2": row["AM2"],
                "AM3": row["AM3"],
                "AM4": row["AM4"],
                "AM5": row["AM5"],
                "MW": int(float(row["MW"])),  # Convert to float first and then to int
                "HTFormPtsStr": row["HTFormPtsStr"],
                "ATFormPtsStr": row["ATFormPtsStr"],
                "HTFormPts": float(row["HTFormPts"]),
                "ATFormPts": float(row["ATFormPts"]),
                "HTWinStreak3": int(row["HTWinStreak3"]),
                "HTWinStreak5": int(row["HTWinStreak5"]),
                "HTLossStreak3": int(row["HTLossStreak3"]),
                "HTLossStreak5": int(row["HTLossStreak5"]),
                "ATWinStreak3": int(row["ATWinStreak3"]),
                "ATWinStreak5": int(row["ATWinStreak5"]),
                "ATLossStreak3": int(row["ATLossStreak3"]),
                "ATLossStreak5": int(row["ATLossStreak5"]),
                "HTGD": int(float(row["HTGD"])),
                "ATGD": int(float(row["ATGD"])),
                "DiffPts": float(row["DiffPts"]),
                "DiffFormPts": float(row["DiffFormPts"])
            })

    with open(json_file_path, "w") as jsonfile:
        json.dump(data, jsonfile, indent=2)

if __name__ == "__main__":
    convert_csv_to_json()