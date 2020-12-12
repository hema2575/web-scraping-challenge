{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Import Dependencies\n",
    "from bs4 import BeautifulSoup as bs\n",
    "from splinter import Browser\n",
    "import requests\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "#choosing the executable path to driver\n",
    "executable_path ={'executable_path': 'chromedriver.exe'}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "#scraping data from the NASA Mars News Site\n",
    "url = 'https://mars.nasa.gov/news/'\n",
    "response = requests.get(url)\n",
    "soup = bs(response.text,'html.parser')\n",
    "\n",
    "#examining results\n",
    "#print(soup.prettify())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NASA to Broadcast Mars 2020 Perseverance Launch, Prelaunch Activities\n",
      "\n",
      "Starting July 27, news activities will cover everything from mission engineering and science to returning samples from Mars to, of course, the launch itself.\n"
     ]
    }
   ],
   "source": [
    "#collecting the latest News Title and Paragraph Text\n",
    "title = soup.find('div', class_= \"content_title\").find('a').text.strip()\n",
    "paragraph_txt = soup.find('div', class_= \"rollover_description_inner\").text.strip()\n",
    "\n",
    "#printing results\n",
    "print(title)\n",
    "print(\"\\n\"+paragraph_txt)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Visit the URL for the JPL Featured Space Image through splinter\n",
    "image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "browser.visit(image_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/spaceimages/images/wallpaper/PIA14925-1920x1200.jpg\n",
      "https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA14925-1920x1200.jpg\n"
     ]
    }
   ],
   "source": [
    "#creating HTML object and parsing\n",
    "html_image = browser.html\n",
    "soup = bs(html_image, 'html.parser')\n",
    "\n",
    "#retreieve the url to the current Featured Mars Image from alt='Polar Vortex in Color', backgroundImage\n",
    "featured_image_sub_url = soup.find('div',class_='carousel_items')('article')[0]['style'].\\\n",
    "    replace('background-image: url(','').replace(');','')[1:-1]\n",
    "\n",
    "#main_url\n",
    "main_url = 'https://www.jpl.nasa.gov'\n",
    "\n",
    "#create the full url \n",
    "featured_image_url = main_url + featured_image_sub_url\n",
    "\n",
    "#print results\n",
    "print(featured_image_sub_url )\n",
    "print(featured_image_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "#using splinter to view the space facts for mars\n",
    "mars_facts_url = 'https://space-facts.com/mars/'\n",
    "browser.visit(mars_facts_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Reading the tables in the url using Pandas\n",
    "mars_tables = pd.read_html(mars_facts_url)\n",
    "\n",
    "#checking to see if there are multiple tables\n",
    "type(mars_tables)\n",
    "\n",
    "#locating table on the page contains our \"Mars Facts\"\n",
    "mars_facts_table = mars_tables[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Value</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Fact</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Equatorial Diameter:</th>\n",
       "      <td>6,792 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Polar Diameter:</th>\n",
       "      <td>6,752 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Mass:</th>\n",
       "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Moons:</th>\n",
       "      <td>2 (Phobos &amp; Deimos)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Orbit Distance:</th>\n",
       "      <td>227,943,824 km (1.38 AU)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Orbit Period:</th>\n",
       "      <td>687 days (1.9 years)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Surface Temperature:</th>\n",
       "      <td>-87 to -5 °C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>First Record:</th>\n",
       "      <td>2nd millennium BC</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Recorded By:</th>\n",
       "      <td>Egyptian astronomers</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                              Value\n",
       "Fact                                               \n",
       "Equatorial Diameter:                       6,792 km\n",
       "Polar Diameter:                            6,752 km\n",
       "Mass:                 6.39 × 10^23 kg (0.11 Earths)\n",
       "Moons:                          2 (Phobos & Deimos)\n",
       "Orbit Distance:            227,943,824 km (1.38 AU)\n",
       "Orbit Period:                  687 days (1.9 years)\n",
       "Surface Temperature:                   -87 to -5 °C\n",
       "First Record:                     2nd millennium BC\n",
       "Recorded By:                   Egyptian astronomers"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#formatting data frame\n",
    "mars_facts=mars_facts_table.rename(columns={0:'Fact',1:'Value'}).set_index('Fact').copy()\n",
    "\n",
    "mars_facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#converting to html\n",
    "mars_facts_html = mars_facts.to_html()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [],
   "source": [
    "#visiting the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.\n",
    "mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "browser.visit(mars_hemisphere_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "#creating HTML object and parsing\n",
    "html_hemisphere_image = browser.html\n",
    "soup = bs(html_hemisphere_image, 'html.parser')\n",
    "\n",
    "# get all the info that contains the image links\n",
    "items = soup.find_all('div', class_='item')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'title': 'Cerberus Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'},\n",
       " {'title': 'Schiaparelli Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'},\n",
       " {'title': 'Syrtis Major Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'},\n",
       " {'title': 'Valles Marineris Hemisphere Enhanced',\n",
       "  'img_url': 'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}]"
      ]
     },
     "execution_count": 42,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# List to collect all hemisphere urls \n",
    "hemisphere_image_urls = []\n",
    "\n",
    "# Store the main_ul \n",
    "hemispheres_main_url = 'https://astrogeology.usgs.gov'\n",
    "\n",
    "#for all the info containing the image links\n",
    "for i in items: \n",
    "    title = i.find('h3').text                                               # image title     \n",
    "    sub_image_url = i.find('a', class_='itemLink product-item')['href']     # image url     \n",
    "    browser.visit(hemispheres_main_url + sub_image_url)     # visiting the storage url     \n",
    "    partial_image_html = browser.html                       # HTML Object for full image url storage website\n",
    "    soup = bs( partial_image_html, 'html.parser')           # Parsing HTML for that specific website     \n",
    "    image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']  # creating full image url\n",
    "    hemisphere_image_urls.append({\"title\" : title, \"img_url\" : image_url}) # Adding to dictionary\n",
    "    \n",
    "\n",
    "# Display hemisphere image urls\n",
    "hemisphere_image_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'Mars_News_Title': 'Valles Marineris Hemisphere Enhanced',\n",
       " 'Mars_News_Paragraph': 'Starting July 27, news activities will cover everything from mission engineering and science to returning samples from Mars to, of course, the launch itself.',\n",
       " 'Mars_Featured_Image': 'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA14925-1920x1200.jpg',\n",
       " 'Mars_Facts': '<table border=\"1\" class=\"dataframe\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Value</th>\\n    </tr>\\n    <tr>\\n      <th>Fact</th>\\n      <th></th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>Equatorial Diameter:</th>\\n      <td>6,792 km</td>\\n    </tr>\\n    <tr>\\n      <th>Polar Diameter:</th>\\n      <td>6,752 km</td>\\n    </tr>\\n    <tr>\\n      <th>Mass:</th>\\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\\n    </tr>\\n    <tr>\\n      <th>Moons:</th>\\n      <td>2 (Phobos &amp; Deimos)</td>\\n    </tr>\\n    <tr>\\n      <th>Orbit Distance:</th>\\n      <td>227,943,824 km (1.38 AU)</td>\\n    </tr>\\n    <tr>\\n      <th>Orbit Period:</th>\\n      <td>687 days (1.9 years)</td>\\n    </tr>\\n    <tr>\\n      <th>Surface Temperature:</th>\\n      <td>-87 to -5 °C</td>\\n    </tr>\\n    <tr>\\n      <th>First Record:</th>\\n      <td>2nd millennium BC</td>\\n    </tr>\\n    <tr>\\n      <th>Recorded By:</th>\\n      <td>Egyptian astronomers</td>\\n    </tr>\\n  </tbody>\\n</table>',\n",
       " 'Mars_Hemisphere_Images': [{'title': 'Cerberus Hemisphere Enhanced',\n",
       "   'img_url': 'https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'},\n",
       "  {'title': 'Schiaparelli Hemisphere Enhanced',\n",
       "   'img_url': 'https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'},\n",
       "  {'title': 'Syrtis Major Hemisphere Enhanced',\n",
       "   'img_url': 'https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'},\n",
       "  {'title': 'Valles Marineris Hemisphere Enhanced',\n",
       "   'img_url': 'https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}]}"
      ]
     },
     "execution_count": 48,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "mars_data = {\n",
    "        \"Mars_News_Title\": title,\n",
    "        \"Mars_News_Paragraph\": paragraph_txt,\n",
    "        \"Mars_Featured_Image\": featured_image_url,\n",
    "       # \"Mars_Weather_Data\": mars_weather,\n",
    "        \"Mars_Facts\": mars_facts_html,\n",
    "        \"Mars_Hemisphere_Images\": hemisphere_image_urls\n",
    "    }\n",
    "mars_data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
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
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
