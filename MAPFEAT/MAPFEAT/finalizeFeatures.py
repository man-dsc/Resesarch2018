# Finalizes the features by selecting only the features that are shared between apps
#
# Ignores features that are not shared by at least X apps that came from a single query
# in order to have results with a higher chance of matching the original topic
#
# Calculates cosine similarity to determine whether a feature is 'shared' between two apps

import ast
import os
import csv
import shutil
import sys

from sklearn.feature_extraction.text import TfidfVectorizer

INPUT_PATH = 'output/features'
OUTPUT_PATH = 'output'


def finalize(sharedBetween):
	print 'Finalizing results by finding common features between apps...\n'

	vect = TfidfVectorizer(min_df=2)

	with open('{}/finalizedFeatures.csv'.format(OUTPUT_PATH), 'wb') as w:
		writer = csv.writer(w)
		for dir in os.listdir(INPUT_PATH):
			if not dir.startswith('.'):
				fFeatures = []
				for file in os.listdir('{}/'.format(INPUT_PATH) + dir):
					mFeatures = set()

					# Get list of features for the query
					with open('{}/{}/{}'.format(INPUT_PATH, dir, file), 'rb') as r:
							reader = csv.reader(r)
							for app in reader:
								coreFeatures = ast.literal_eval(app[-2])
								for c in coreFeatures:
									mFeatures.add(' '.join(c))
		                	r.close()

		            # Find the features that are shared between multiple apps that came from that query
					for i1, f1 in enumerate(mFeatures):
						appCount = 0
						for i2, f2 in enumerate(mFeatures):
							if i1 != i2:
								try:
									tfidf = vect.fit_transform([f1, f2])
								except:
									continue

								# Calculate cosine similarity
								a = (tfidf * tfidf.T).A[0][1]

								# If the cosine similarity is above this threshold, we consider it to
								# be 'shared' between these two apps
								if a > 0.6:
									appCount += 1

							# If the feature is shared between enough apps, select it
							if (appCount >= sharedBetween):
								if f1 and f1 not in fFeatures:
									fFeatures.append(f1)

				# Write the finalized features to file
				writer.writerow([dir, ', '.join(fFeatures)])
		w.close()


if __name__ == "__main__":
	sharedBetween = input("\nEnter the minimum number of apps per query that should share each feature: ")
	finalize(sharedBetween)
