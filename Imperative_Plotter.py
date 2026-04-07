import pandas as pd
import matplotlib.pyplot as plt

input_name = input("1 Peter, Ephesians, or Romans?")

if input_name == '1 Peter' or input_name == '1 Pet' or input_name == '1 P':
    file_name = "1Peter.csv"
    book_title = '1 Peter'
elif input_name == 'Ephesians' or input_name == 'Eph' or input_name == 'E':
    file_name = "Ephesians.csv"
    book_title = 'Ephesians'
elif input_name == 'Romans' or input_name == 'Rom' or input_name == 'R':
    file_name = "Romans.csv"
    book_title = 'Romans'

# Load your data
file_path = file_name  # change path if needed
df = pd.read_csv(file_path, header=None, names=["Chapter", "VerseInChapter", "VerseNum", "Imperative", "Count"])

# --- CLEAN DATA ---
df['Chapter'] = df['Chapter'].ffill()  # fill down missing chapter names
df['Count'] = pd.to_numeric(df['Count'], errors='coerce').fillna(0).astype(int)

# Simplify chapter name (remove "Chapter " text)
df['ChapterNum'] = df['Chapter']#.str.extract(r'(\d+)').astype(int)
df['Reference'] = df['ChapterNum']#.astype(str) + ':' + df['VerseInChapter'].astype(str) 

# --- PLOT ---
plt.figure(figsize=(14, 8.5))
plt.title("Imperatives Across the Book of %s" % book_title, fontsize=18, weight='bold', pad=20)
plt.xlim([1, len(df['Count'])]) # plot the length of the book
plt.xlabel("Verse number", fontsize=12)
plt.ylabel("Imperatives per verse", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.3, zorder=1)

# --- ADD CHAPTER LINES AND LABELS ---
chapter_starts = df[df['VerseInChapter'] == 1][['ChapterNum', 'VerseNum']]
for _, row in chapter_starts.iterrows():
    plt.axvline(x=row['VerseNum'], color='gray', linestyle='--', alpha=0.6)
    plt.text(row['VerseNum'] + 1, max(df['Count']) + 0.2, f"{row['ChapterNum']}",
             rotation=0, va='bottom', ha='left', fontsize=14, color='gray', weight='bold')

# --- ADD IMPERATIVE LABELS (LARGER + RED) ---
for _, row in df.iterrows():
    if row['Imperative'] and str(row['Imperative']).strip() != "":
        plt.text(
            row['VerseNum'], row['Count'] + 0.1, str(row['Imperative']),
            rotation=90, va='bottom', ha='center',
            fontsize=14, color='firebrick', fontweight='bold'
        )

# Remove dots/lines and tidy up space
plt.ylim(0.8, max(df['Count']) + 1.5)
plt.show()