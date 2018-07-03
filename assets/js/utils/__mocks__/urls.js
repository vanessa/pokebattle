const Urls = {
  'api-battles:battle-list': () => 'https://pokebattle.com/api/battles/',
  'api-battles:battle-details': params => `https://pokebattle.com/api/battles/${params.pk}`,
  'api-users:user-details': () => 'https://pokebattle.com/api/user-details',
  'battles:team': params => `https://pokebattle.com/battles/details/${params.pk}/team`,
};

export default Urls;
