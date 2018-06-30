const capitalizeFirst = name => (
  String(name).charAt(0).toUpperCase() + String(name).substring(1)
);

export default capitalizeFirst;
