# UnifiedImageReader

```mermaid
classDiagram
    Image *-- ImageReader
    ImageReader *-- Adapter
    Adapter <|-- VIPS
    Adapter <|-- SlideIO
    class Image {
        get_region()
        number_of_regions()
    }
    class ImageReader {
        get_region()
        number_of_regions()
        validate_region()
        region_index_to_coordinates()
    }
    class Adapter {
        <<abstract>>
        get_region()
        get_width()
        get_height()
    }
```

## Installation

All of the dependencies for the adapters require manual installation because of the dll dependencies. Contact Adin at adinbsolomon@gmail.com with any questions.
