namespace php RPC

service DemoService
{
  string hello(),
  string world(1:string type)
}
