export interface VisionInspectionBoundingBoxVertice {
    x: number;
    y: number;
}

export interface VisionInspectionPage {
    name: string;
    url: string;
}

export interface VisionInspectionLandmarkLocation {
    latitude: number;
    longitude: number;
}

export interface VisionInspectionLandmark {
    name: string;
    url: string;
    location?: VisionInspectionLandmarkLocation;
}

export interface VisionInspectionWord {
    text: string;
    vertices: VisionInspectionBoundingBoxVertice[];
    language_code?: string;
    language_name?: string;
}

export default interface VisionInspection {
    pages: VisionInspectionPage[];
    words: VisionInspectionWord[];
    labels: string[];
    keywords: string[];
    landmarks: VisionInspectionLandmark[];
}
