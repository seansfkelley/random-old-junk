//
//  InputManagerController.m
//  MulitClutch
//
//  Created by William Henderson on 2/10/08.
//  Copyright 2008 __MyCompanyName__. All rights reserved.
//  Multiclutch is made available for use under the BSD license.
//

#import "InputManagerInstaller.h"


@implementation InputManagerInstaller

-(void)installInputManager {
	NSLog(@"[MultiClutch] Launching installer helper...");
	
	NSString *filePath = [[NSBundle bundleWithIdentifier:@"com.wonderboots.multiclutchprefpanel"] pathForResource:@"InputManagerInstallerHelper.app" ofType:nil];
	NSURL *fileURL = [[NSURL alloc] initFileURLWithPath:filePath];
	[[NSWorkspace sharedWorkspace] openURL:fileURL];
	[NSApp terminate:self];
	[fileURL release];
}
 
@end