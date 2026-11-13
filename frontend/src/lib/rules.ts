export const isIfsc = (value: string) => /^[A-Z]{4}0[A-Z0-9]{6}$/.test(value.trim().toUpperCase());
export const isMobile = (value: string) => /^[6-9]\d{9}$/.test(value.trim());
export const isPinCode = (value: string) => /^\d{6}$/.test(value.trim());
export const isAadhaar = (value: string) => /^\d{12}$/.test(value.replace(/\s/g, ""));
export const isLengthInRange = (value: string, min: number, max: number) => value.trim().length >= min && value.trim().length <= max;
