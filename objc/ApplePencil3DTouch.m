// http://www.ifun.de/ipad-pro-hack-3d-touch-mit-dem-apple-pencil-85131/

// https://gist.github.com/hamzasood/02e6e87835a17f4e1b9e

#import <UIKit/UIKit.h>
#import <objc/runtime.h>

// Hook with ObjC runtime functions
%config(generator=internal)

// New methods created below
@interface UIGestureRecognizer ()
+ (void)hs_beginForcingAllNewGestureRecognizersToAllowPencilInput;
+ (void)hs_endForcingAllNewGestureRecognizersToAllowPencilInput;
@end
@interface UITouch ()
- (BOOL)hs_shouldScaleForceValuesFromPencilLandTo3DTouchLand;
- (void)hs_setShouldScaleForceValuesFromPencilLandTo3DTouchLand:(BOOL)newShouldScale;
@end




%hook UIDevice

/*
    Needed so that -[UITraitCollection forceTouchCapability] returns true.
    While this isn't needed for the actual 3D Touch interactions, most apps won't register for previewing unless this returns true.
*/
- (BOOL)_supportsForceTouch {
    return YES;
}

%end




%hook UIPreviewInteractionController

/*
    By default, the 3D Touch gesture recognizers will only respond to direct touches.
    Override the gesture recognizers creation point to force them all to also accept pencil input (see UIGestureRecognizer hooks below)
*/
- (void)initGestureRecognizers {
    [UIGestureRecognizer hs_beginForcingAllNewGestureRecognizersToAllowPencilInput];
    %orig;
    [UIGestureRecognizer hs_endForcingAllNewGestureRecognizersToAllowPencilInput];
}

%end




%hook UIGestureRecognizer

static BOOL _shouldForceNewGestureRecognizersToAllowPencilInput;

%new
+ (void)hs_beginForcingAllNewGestureRecognizersToAllowPencilInput {
    _shouldForceNewGestureRecognizersToAllowPencilInput = YES;
}

- (void)setAllowedTouchTypes:(NSArray<NSNumber *> *)allowedTouchTypes {
    if (_shouldForceNewGestureRecognizersToAllowPencilInput && ![allowedTouchTypes containsObject:@(UITouchTypeStylus)]) {
        allowedTouchTypes = [allowedTouchTypes arrayByAddingObject:@(UITouchTypeStylus)];
    }
    %orig(allowedTouchTypes);
}

%new
+ (void)hs_endForcingAllNewGestureRecognizersToAllowPencilInput {
    _shouldForceNewGestureRecognizersToAllowPencilInput = NO;
}


/*
    See UITouch hooks below for definition and explanation of hs_shouldScaleForceValuesFromPencilLandTo3DTouchLand.
*/
- (void)_updateForceClassifierWithEvent:(UIEvent *)event {
    for (UITouch *touch in [event touchesForGestureRecognizer:self]) {
        [touch hs_setShouldScaleForceValuesFromPencilLandTo3DTouchLand:YES];
    }
    %orig;
}

%end




%hook UITouch

static char *ShouldScaleKey = "ShouldScaleForceValuesFromPencilLandTo3DTouchLand";

%new
- (BOOL)hs_shouldScaleForceValuesFromPencilLandTo3DTouchLand {
    return [objc_getAssociatedObject(self, ShouldScaleKey) boolValue];
}

%new
- (void)hs_setShouldScaleForceValuesFromPencilLandTo3DTouchLand:(BOOL)newShouldScale {
    objc_setAssociatedObject(self, ShouldScaleKey, @(newShouldScale), OBJC_ASSOCIATION_COPY_NONATOMIC);
}

/*
    Force values from Apple Pencil are on a slightly different scale to those from a regular touch on a 3D Touch display.
    By scaling up the pressure values a bit, you won't have to press as hard with the pencil to trigger 3D Touch.
*/
- (CGFloat)_pressure {
    CGFloat pressure = %orig;
    if (self.type == UITouchTypeStylus && self.hs_shouldScaleForceValuesFromPencilLandTo3DTouchLand) {
        pressure *= 2.25;
    }
    return pressure;
}

%end