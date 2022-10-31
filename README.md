# UnifiedImageReader

```mermaid
classDiagram
    Image *-- ImageReader
    ImageReader <|-- ImageReaderAdaptive
    ImageReader <|-- ImageReaderDirectory
    ImageReaderAdaptive *-- Adapter
    Adapter <|-- VIPS
    Adapter <|-- SlideIO
    class Image {
        get_region()
        number_of_regions()
    }
    class ImageReader {
        <<abstract>>
        get_region()
        number_of_regions()
    }
    class ImageReaderAdaptive {
        get_region()
        number_of_regions()
    }
    class ImageReaderDirectory {
        get_region()
        number_of_regions()
    }
    class Adapter {
        <<abstract>>
        get_region()
        get_width()
        get_height()
    }
```

## Installation

All of the dependencies for the adapters require manual installation because of the dll dependencies. It is recommended that you use the dev-container with VSCode because this is handled already. Contact Adin at adinbsolomon@gmail.com with any questions.
