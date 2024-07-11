
const ApiController = {
  async fetchData(req, res, next) {
    try {
      
      return next();
    } catch {
      return next({
        err: "error in fetchData controller",
      });
    }
  },

};
export default ApiController;