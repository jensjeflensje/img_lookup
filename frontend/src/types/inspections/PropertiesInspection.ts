export interface PropertiesInspectionHashes {
    md5: string;
    sha256: string;
}

export default interface PropertiesInspection {
    width: number;
    height: number;
    hash: PropertiesInspectionHashes;
}
