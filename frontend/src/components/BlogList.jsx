import BlogCard from './BlogCard'; const BlogList=({posts})=><div className="blog-grid">{posts.map(p=><BlogCard key={p.id} post={p}/>)}</div>; export default BlogList;
