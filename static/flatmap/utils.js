function scrollParentToChild(parent, child) {

	// Where is the parent on page
	var parentRect = parent.getBoundingClientRect();
	// What can you see?
	var parentViewableArea = {
		height: parent.clientHeight,
		width: parent.clientWidth
	};

	var parentBottom = parentRect.top + parentViewableArea.height;
  
	// Where is the child
	var childRect = child.getBoundingClientRect();
	// Is the child viewable?
	var isViewable = ((childRect.top >= parentRect.top) && 
					(childRect.bottom <= parentBottom));
	
	// if you can't see the child try to scroll parent
	if (!isViewable) {

		// Should we scroll using top or bottom? Find the smaller ABS adjustment
		const scrollTop = childRect.top - parentRect.top;
		const scrollBot = childRect.bottom - parentBottom;
		if (Math.abs(scrollTop) < Math.abs(scrollBot)) {
			// we're near the top of the list
			parent.scrollTop += scrollTop;
		} else {
			// we're near the bottom of the list
			parent.scrollTop += scrollBot;
		}
	}
  
  }