'''
Sample colours from selected image and overlay selected colours along bottom edge of image.
For use in Pythonista

UI selector borrowed directly from Ole Zorn @olemoritz: https://gist.github.com/omz/ae96874dfbda54ed2771
'''
import photos
import Image
import random
import ui
import console
import clipboard

colourcount = 25 # Number of selectable samples
samplesize = 400 # Size of downsampled image. Reduce this for a smaller sample set. Results in colours being lost through pixelation.


selected_image = photos.pick_image() # Get image. Comment this line and uncomment the next line to use camera instead.
# selected_image = photos.capture_image()
select_width, select_height = selected_image.size # These will be used for final colour chip placement.


sample = selected_image.resize((samplesize,samplesize)) # Reduce available colours by reducing a copy of and pixelating the image.
colors = sorted(sample.getcolors(samplesize*samplesize)) # Remove duplicate colours.
colors = random.sample(colors,  colourcount)  # Get random selection of colours from sample image.


selected_colors = []
def tapped(sender):
	r, g, b, a = sender.background_color
	select_color = (int(r*255), int(g*255), int(b*255))
	# If border colour is active, remove colour from selected_colors. Otherwise, add it.
	if sender.border_color == (0.0,1.0,0.0,1.0):
		sender.border_width=0
		sender.border_color='#000000'
		selected_colors.remove(select_color)
	else: 
		sender.border_width=15
		sender.border_color='#00ff00'
		selected_colors.append(select_color)
	console.hud_alert(str(len(selected_colors)) + ' in queue') # Tell us how many colours are selected.


def save_action(sender):
	scroll_view.close() # Close the view. Is this really the best place for this?
	chipsize = select_width/len(selected_colors) 
	for i, c in enumerate(selected_colors):
		bar = (chipsize*i, select_height-chipsize, (chipsize*i)+chipsize, select_height)
		selected_image.paste(c, bar)
	selected_image.show()
	saveit = photos.save_image(selected_image)
	
	if saveit is True:
		console.hud_alert('Sampled image has been saved')
	elif saveit is False:
		console.hud_alert('Uh oh, not saved')


#Add buttons for all the colors to a scroll view:
scroll_view = ui.ScrollView(frame=(0, 0, 400, 400))
scroll_view.content_size = (0, len(colors) * 80)
for i, c in enumerate(colors):
	r, g, b = c[1]
	color = (float(r/255.0),float(g/255.0),float(b/255.0))
	swatch = ui.Button(frame=(0, i*80, 400, 80), background_color=color)
	swatch.title = str(c[1])
	swatch.flex = 'w'
	swatch.action = tapped
	scroll_view.add_subview(swatch)
scroll_view.name = 'Random Color Picker'
save_button = ui.ButtonItem()
save_button.title = 'Save'
save_button.action = save_action
save_button.tint_color = 'red'
scroll_view.right_button_items = [save_button]
scroll_view.present('sheet')



