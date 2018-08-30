//
//  AppController.m
//  GraphKitDemo
//
//  Created by Dave Jewell on 06/11/2008.
//  Copyright 2008 Cocoa Secrets. All rights reserved.
//

#import "AppController.h"

@implementation AppController

- (void) createDummyData
{
	_dummyNumbers = [[NSArray arrayWithObjects:	[NSNumber numberWithDouble: 5.3],
																							[NSNumber numberWithDouble: 3.1],
																							[NSNumber numberWithDouble: 17.6],
																							[NSNumber numberWithDouble: 7.4],
																							[NSNumber numberWithDouble: 9.0], 
																							nil] retain];
	
	_dummyColors =	[[NSArray arrayWithObjects:	[NSColor blueColor],
																							[NSColor grayColor],
																							[NSColor greenColor],
																							[NSColor redColor],
																							[NSColor yellowColor], 
																							nil] retain];
}

- (Class) dataSetClass
{
	// Available: GRXYDataSet, GRPieDataSet, GRAreaDataSet, GRLineDataSet, GRColumnDataSet
	return [GRColumnDataSet class];
}

- (void) awakeFromNib
{
	[self createDummyData];
	
	GRDataSet * dataSet = [[[self dataSetClass] alloc] initWithOwnerChart: _chartView];
	[dataSet setProperty: [NSNumber numberWithInt: 1] forKey: GRDataSetDrawPlotLine];
	[dataSet setProperty: [NSNumber numberWithInt: 90] forKey: GRDataSetPieStartAngle];
	
	[_chartView setProperty: [NSNumber numberWithInt: 0] forKey: GRChartDrawBackground];
	
	// Force the Y-axis to display from zero
	GRAxes * axes = [_chartView axes];
	[axes setProperty: [NSNumber numberWithInt: 0] forKey: @"GRAxesYPlotMin"];
	[axes setProperty: [NSNumber numberWithInt: 1] forKey: @"GRAxesFixedYPlotMin"];
	
	[_chartView addDataSet: dataSet loadData: YES];
	[dataSet release];
}

// Delegate methods for GRChartView

- (NSInteger) chart: (GRChartView *) chartView numberOfElementsForDataSet: (GRDataSet *) dataSet
{
	return [_dummyNumbers count];
}

- (double) chart: (GRChartView *) chartView yValueForDataSet: (GRDataSet *) dataSet element: (NSInteger) element
{
	return [[_dummyNumbers objectAtIndex: element] doubleValue];
}

- (NSColor *) chart: (GRChartView *) chartView colorForDataSet: (GRDataSet *) dataSet element: (NSInteger) element
{
	return [_dummyColors objectAtIndex: element];
}

@end
