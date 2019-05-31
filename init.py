import pickle
file = open('store.pckl', 'wb')
pickle.dump(0, file)  # score
pickle.dump(100, file)  # limit
pickle.dump(1, file)  # speed
pickle.dump(1.7, file)  # alpha
file.close()
