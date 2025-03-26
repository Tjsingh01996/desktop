package main

import (
	"image"
	"image/color"
	"image/jpeg"
	"log"
	"os"
)

func main1() {
	// Open the input image
	inputFile, err := os.Open("./input.png")
	if err != nil {
		log.Fatalf("Failed to open input image: %v", err)
	}
	defer inputFile.Close()

	// Decode the image
	srcImage, _, err := image.Decode(inputFile)
	if err != nil {
		log.Fatalf("Failed to decode image: %v", err)
	}

	// Get the image bounds
	bounds := srcImage.Bounds()

	// Create a new image with the same size as the source image
	outputImage := image.NewRGBA(bounds)

	// Copy pixels from the source image to the output image
	for y := bounds.Min.Y; y < bounds.Max.Y; y++ {
		for x := bounds.Min.X; x < bounds.Max.X; x++ {
			outputImage.Set(x, y, srcImage.At(x, y))
		}
	}

	// Add a simple watermark (a solid rectangle)
	addWatermark(outputImage, bounds)

	// Save the watermarked image to a new file
	outputFile, err := os.Create("output.jpg")
	if err != nil {
		log.Fatalf("Failed to create output image: %v", err)
	}
	defer outputFile.Close()

	err = jpeg.Encode(outputFile, outputImage, nil)
	if err != nil {
		log.Fatalf("Failed to encode image: %v", err)
	}

	log.Println("Watermarked image saved as output.jpg")
}

// addWatermark adds a simple rectangle as a watermark
func addWatermark(img *image.RGBA, bounds image.Rectangle) {
	// Define the rectangle area for the watermark
	startX := bounds.Max.X - 200 // Position the watermark at the bottom-right
	startY := bounds.Max.Y - 50
	endX := bounds.Max.X
	endY := bounds.Max.Y

	// Define the watermark color (semi-transparent white)
	watermarkColor := color.RGBA{R: 255, G: 128, B: 0, A: 255}

	// Modify the pixels in the rectangle area
	for y := startY; y < endY; y++ {
		for x := startX; x < endX; x++ {
			img.Set(x, y, watermarkColor)
		}
	}
}
