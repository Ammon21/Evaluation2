import os
import pandas as pd
import re

# Label encoding map
rating_map = {
    "– Excellent": 5,
    "– Very Good": 4,
    "– Good": 3,
    "– Fair": 2,
    "– Unsatisfactory": 1
}

# Root directory path
root_dir = "Teachers Evaluation-2025-Second round"
merged_data = []

if not os.path.exists(root_dir):
    print(f"❌ Root directory not found: {root_dir}")
else:
    print(f"✅ Found root directory: {root_dir}")

# Traverse grade and section folders
for grade_folder in os.listdir(root_dir):
    grade_path = os.path.join(root_dir, grade_folder)
    if not os.path.isdir(grade_path):
        continue

    grade_match = re.search(r"(\d+)", grade_folder)
    if not grade_match:
        continue
    grade = int(grade_match.group(1))

    for section_folder in os.listdir(grade_path):
        section_path = os.path.join(grade_path, section_folder)
        if not os.path.isdir(section_path):
            continue

        section_match = re.search(r"Section-([A-C])", section_folder)
        if not section_match:
            continue
        section = section_match.group(1)

        for filename in os.listdir(section_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(section_path, filename)
                print(f"📄 Processing: {file_path}")

                # Extract teacher name from filename
                teacher_match = re.search(r"\((.*?)\)", filename)
                teacher = teacher_match.group(1) if teacher_match else "Unknown"

                try:
                    df = pd.read_csv(file_path)

                    # Label encode
                    df = df.replace(rating_map)

                    # Add metadata
                    df["Grade"] = grade
                    df["Section"] = section
                    df["Teacher"] = teacher

                    merged_data.append(df)

                except Exception as e:
                    print(f"❌ Failed to process file: {file_path}\nReason: {e}")

# Final merge
if merged_data:
    final_df = pd.concat(merged_data, ignore_index=True)
    final_df.to_csv("merged_teacher_evaluations.csv", index=False)
    print("✅ All files merged and saved as 'merged_teacher_evaluations.csv'")
else:
    print("❌ No data merged. Check file formats and folders.")
