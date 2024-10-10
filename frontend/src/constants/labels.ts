import randomColor from 'randomcolor';

const generatedColors = new Set<string>();

export const getUniqueColor = (index: number, totalColors: number) => {
  let color;
  const hue = (index * (360 / totalColors)) % 360;
  do {
    color = randomColor({ luminosity: 'dark', format: 'rgb', hue });
  } while (generatedColors.has(color));
  generatedColors.add(color);
  return color;
};

const totalPatientColors = 7; // Number of colors needed for patientInformation
const totalOrganizationColors = 3; // Number of colors needed for organizationInformation

export const LABELS = {
  patientInformation: {
    title: "Patient Information",
    items: [
      { name: "First Name", required: true, color: getUniqueColor(0, totalPatientColors) },
      { name: "Last Name", required: true, color: getUniqueColor(1, totalPatientColors) },
      { name: "DOB", required: false, color: getUniqueColor(2, totalPatientColors) },
      { name: "Gender", required: false, color: getUniqueColor(3, totalPatientColors) },
      { name: "Phone Number", required: false, color: getUniqueColor(4, totalPatientColors) },
      { name: "Email", required: false, color: getUniqueColor(5, totalPatientColors) },
      { name: "Address", required: false, color: getUniqueColor(6, totalPatientColors) },
    ],
  },
  organizationInformation: {
    title: "Organization Information",
    items: [
      { name: "Name", required: true, color: getUniqueColor(0, totalOrganizationColors) },
      { name: "Email", required: false, color: getUniqueColor(1, totalOrganizationColors) },
      { name: "Address", required: false, color: getUniqueColor(2, totalOrganizationColors) },
    ],
  },
};