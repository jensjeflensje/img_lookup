interface CleanedMetadata {
    latitude?: number;
    longitude?: number;
    device?: string;
}

export default interface MetadataInspection {
    cleaned: CleanedMetadata;
    exif: object;
}
