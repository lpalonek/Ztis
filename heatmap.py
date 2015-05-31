import csv
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib as mpl

# import Image


class HeatMap:

	def __init__(self, collection):
		self.collection = collection

	def setMap(self, mapFileName):
		cmap = mpl.cm.Blues
		shapename = 'admin_0_countries'
		countries_shp = shpreader.natural_earth(resolution='110m',
												category='cultural', name=shapename)
		fig, ax = plt.subplots(figsize=(12,6),
					   subplot_kw={'projection': ccrs.Robinson()})

		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


		countriesRecords = shpreader.Reader(countries_shp).records()
		countryMap = self.createDict(countriesRecords)

		maxQuantity = max(countryMap.values())
		for country in shpreader.Reader(countries_shp).records():
			countryName = country.attributes['name_long']
			quantity = countryMap[countryName]

			ax.add_geometries(country.geometry, ccrs.PlateCarree(),
							  facecolor=cmap(quantity / float(maxQuantity), 1),
							  label=countryName)
		norm = mpl.colors.Normalize(vmin = 1, vmax = maxQuantity)
		cax = fig.add_axes([0.91, 0.1, 0.02, 0.8])
		mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm )


		print(maxQuantity)
		plt.savefig(mapFileName, dpi = 200)

	def createDict(self, countriesRecords):
		dictionary = {}
		result = {}
		for item in list(self.collection):
			name = item['_id']
			value = item['value']
			dictionary[str(name)] = value
		for country in countriesRecords:
			countryLongName = country.attributes['name_long']
			postalValue, countryValue = 0, 0
			postalCode = country.attributes['postal']
			if dictionary.__contains__(postalCode):
				postalValue = dictionary[postalCode]
			if dictionary.__contains__(countryLongName):
				countryValue = dictionary[countryLongName]

			if result.__contains__(countryLongName):
				result[countryLongName] = postalValue + countryValue + result[countryLongName]
			result[countryLongName] = postalValue + countryValue
		# ugly hack mode on
		result['United Kingdom'] += dictionary['UK']
		# ugly hack mode off
		return result





